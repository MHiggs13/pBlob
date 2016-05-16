package com.mh.blobageddon;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;

/**
 * TODO: document your custom view class.
 */
public class GunnerView extends SurfaceView {

    public Connection connection;
    private SurfaceHolder holder;
    private GunnerLoopThread gunnerLoopThread;
    private Thumbstick thumbstick;
    private FireButton fireButton;

    // x and y values of the touch of the player
    public float x = 0, y = 0, lastX = x, lastY = y;

    private static final int INVALID_POINTER_ID = -1;
    private int thumbstickId= INVALID_POINTER_ID, fireButtonId = INVALID_POINTER_ID;

    private Move move;

    public GunnerView(Context context) {
        super(context);
        this.connection = Helper.conn;
        move = new Move(x, y);

        thumbstick = new Thumbstick(context);
        fireButton = new FireButton(context);

        holder = getHolder();
        holder.addCallback(new SurfaceHolder.Callback() {
            @Override
            public void surfaceDestroyed(SurfaceHolder holder) {
                boolean retry = true;
                gunnerLoopThread.setRunning(false);
                while (retry) {
                    try {
                        gunnerLoopThread.join();
                        retry = false;
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void surfaceCreated(SurfaceHolder holder) {
                gunnerLoopThread = new GunnerLoopThread(GunnerView.this);
                gunnerLoopThread.setRunning(true);
                gunnerLoopThread.start();
            }

            @Override
            public void surfaceChanged(SurfaceHolder holder, int format,
                                       int width, int height) {
                }
        });

    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        int action = event.getAction();

        switch (action & MotionEvent.ACTION_MASK) {

            case MotionEvent.ACTION_DOWN: {

                float x = event.getX(0);
                float y = event.getY(0);

                final int pointerId = event.getPointerId(0);  // ACTION_DOWN = one pointer so index 0

                if (thumbstick.touchRegion.isXYIn(x, y)) {
                    thumbstick.onMove(event, pointerId);
                    thumbstickId = pointerId;
                }
                else if (fireButton.touchRegion.isXYIn(x, y)) {
                    fireButton.onDown();
                    fireButtonId = pointerId;
                }
                break;
            }

            case MotionEvent.ACTION_POINTER_DOWN: {

                int index = (action & MotionEvent.ACTION_POINTER_INDEX_MASK)
                        >> MotionEvent.ACTION_POINTER_INDEX_SHIFT;
                final int pointerId = event.getPointerId(index);

                float x = event.getX(index);
                float y = event.getY(index);

                if (thumbstick.touchRegion.isXYIn(x, y)) {
                    thumbstick.onMove(event, pointerId);
                    thumbstickId = pointerId;
                }
                else if (fireButton.touchRegion.isXYIn(x, y)) {
                    fireButton.onDown();
                    fireButtonId = pointerId;
                }
                break;
            }

            case MotionEvent.ACTION_UP: {
                final int pointerId = event.getPointerId(0);

                if (thumbstickId == pointerId) {
                    thumbstick.onUp();
                    thumbstickId = INVALID_POINTER_ID;
                }
                else if (fireButtonId == pointerId) {
                    fireButton.onUp();
                    fireButtonId = INVALID_POINTER_ID;
                }
                break;
            }

            case MotionEvent.ACTION_POINTER_UP: {
                final int index = (action & MotionEvent.ACTION_POINTER_INDEX_MASK)
                        >> MotionEvent.ACTION_POINTER_INDEX_SHIFT;
                final int pointerId = event.getPointerId(index);

                if (thumbstickId == pointerId) {
                    thumbstick.onUp();
                    System.out.println("thumstickACTIONUP");
                }
                else if (fireButtonId == pointerId) {
                    fireButton.onUp();
                }
                // if either Id is the one being released find new primary id
                if (thumbstickId == pointerId) {
                    final int newPointerIndex = index == 0 ? 1 : 0;
                    lastX = event.getX(newPointerIndex);
                    lastY = event.getY(newPointerIndex);
                    fireButtonId = event.getPointerId(newPointerIndex);
                }
                else if(fireButtonId == pointerId) {
                    final int newPointerIndex = index == 0 ? 1 : 0;
                    lastX = event.getX(newPointerIndex);
                    lastY = event.getY(newPointerIndex);
                    thumbstickId = event.getPointerId(newPointerIndex);
                }
                break;
            }

            case MotionEvent.ACTION_MOVE: {
                // use thumbstickID to find index as thumbstick is only one that requires movement
                final int index = event.findPointerIndex(thumbstickId);

                if (index != -1) {
                    thumbstick.onMove(event, thumbstickId);
                }
                break;
            }
        }
        return true;
    }

    private void changeMainScreenActivity () {
        final Context context = GunnerView.this.getContext();
        Intent intent = new Intent(context , GunnerView.class);
        context.startActivity(intent);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        thumbstick.onDraw(canvas);
        fireButton.onDraw(canvas);
    }

    /**
     * Method that focusing on updating parts of the activity that aren't
     * focused on drawing. Makes sure a connection is kept alive between
     * the server and this particular client
     */
    protected void update() {
        if (connection.isConnected) {
            int fireTally = fireButton.getFireTally();
//            System.out.println("TALLY: " + fireTally);
            connection.sendGun(fireTally + "," + thumbstick.getAngle() + ";");
        } else {      //attempt to reconnect
            connection.setupSocket();
        }
    }

private class GunnerLoopThread extends Thread {
    private GunnerView view;
    private boolean running = false;

    public GunnerLoopThread(GunnerView view) {
        this.view = view;
    }

    public boolean getRunning() {
        return running;
    }

    public void setRunning(boolean run) {
        running = run;
    }

    @Override
    public void run() {
        while (running) {
            Canvas c = null;
            try {
                c = view.getHolder().lockCanvas();
                synchronized (view.getHolder()) {
                    view.update();
                    if (c != null) {
                        view.onDraw(c);
                    }
                    if (connection.getGState() == GState.MAIN_SCREEN) {
                        changeMainScreenActivity();
                        running = false;
                    }
                }
            } finally {
                if (c != null) {
                    view.getHolder().unlockCanvasAndPost(c);
                }
            }
        }
    }
}
}

