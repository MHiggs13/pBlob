package com.mh.blobageddon;

import android.content.Context;
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

    private Connection connection;
    private SurfaceHolder holder;
    private GunnerLoopThread gunnerLoopThread;
    private Thumbstick thumbstick;
    private FireButton fireButton;

    // x and y values of the touch of the player
    public float x = 0, y = 0;

    private Move move;

    public GunnerView(Context context) {
        super(context);
        this.connection = Helper.conn;
        move = new Move(x, y);

        thumbstick = new Thumbstick(context);
        fireButton = new FireButton(context);

        this.setOnTouchListener(new OnTouchListener() {
            private int mActivePointerId;
            @Override
            public boolean onTouch(View v, MotionEvent event) {

                int action = event.getAction();

                switch (action & MotionEvent.ACTION_MASK) {

                    case MotionEvent.ACTION_DOWN: {
                        int id = event.getPointerId(0);

                        float x = event.getX(0);
                        float y = event.getY(0);

                        if (fireButton.touchRegion.isXYIn(x, y)) {
                            fireButton.onTouch(event);
                        }
                        break;
                    }

                    case MotionEvent.ACTION_POINTER_DOWN: {
                        int index = event.getActionIndex();
                        int id = event.getPointerId(index);

                        float x = event.getX(index);
                        float y = event.getY(index);

                        if (thumbstick.touchRegion.isXYIn(x, y)) {
                            thumbstick.onTouch(event);
                        }
                        if (fireButton.touchRegion.isXYIn(x, y)) {
                            fireButton.onTouch(event);
                        }
                        break;
                    }

                    case MotionEvent.ACTION_UP: {
                        int index = event.getActionIndex();

                        float x = event.getX(index);
                        float y = event.getY(index);

                        if (thumbstick.touchRegion.isXYIn(x, y)) {
                            thumbstick.onTouch(event);
                        }
                        if (fireButton.touchRegion.isXYIn(x, y)) {
                            fireButton.onTouch(event);
                        }
                        break;
                    }

                    case MotionEvent.ACTION_POINTER_UP: {
                        int index = event.getActionIndex();

                        float x = event.getX(index);
                        float y = event.getY(index);

                        if (thumbstick.touchRegion.isXYIn(x, y)) {
                            thumbstick.onTouch(event);
                        }
                        if (fireButton.touchRegion.isXYIn(x, y)) {
                            fireButton.onTouch(event);
                        }
                        break;
                    }

                    case MotionEvent.ACTION_MOVE: {
                        int index = event.getActionIndex();

                        float x = event.getX(index);
                        float y = event.getY(index);

                        if (thumbstick.touchRegion.isXYIn(x, y)) {
                            thumbstick.onTouch(event);
                        }
                        break;
                    }
                }

                return true;
            }
        });

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
            System.out.println("TALLY: " + fireTally);
            connection.sendMessage(fireTally + ", " + thumbstick.getAngle() + ";");
        } else {      //attempt to reconnect
            connection.setupSocket();
        }
    }
}


class GunnerLoopThread extends Thread {
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
                }
            } finally {
                if (c != null) {
                    view.getHolder().unlockCanvasAndPost(c);
                }
            }
        }
    }

}

