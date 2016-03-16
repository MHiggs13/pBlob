package com.mh.blobageddon;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.FloatMath;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;

/**
 * Created by michaelh on 01/02/2016.
 */
public class MoveControllerView extends SurfaceView {

    private Connection connection;

    private SurfaceHolder holder;
    private Bitmap bmpBall, bmpBallBG;
    private GameLoopThread gameLoopThread;

    // Original x and y values of bmpBall part of the thumb stick
    public float x = 0, y = 0;

    // zX and zY are the default values of bmpBall, in this case the center of the canvas (width/2, height/2)
    private int zX, zY;

    // dX and dY are the difference between zeroX and x, zeroY and y
    // hyp is the distance from zX and zY to the center of bmpBall,
    // used to disallow bmpBall from going out of bounds of bmpBallBG
    // angle is the angle of the hypotenuse
    private float dX, dY, hyp, angle;
    private Move move;

    public MoveControllerView(Context context) {
        super(context);
        this.connection = Helper.conn;
        move =  new Move(x, y);

        this.setOnTouchListener(new OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                // Update x and y based on touch from user
                x = event.getX();
                y = event.getY();

                // Set dX and dY equal to distance away from center of screen
                dX = x - zX;
                dY = y - zY;

                int radius = bmpBall.getWidth()-200;

                // Check if bmpBall goes out of bounds and fix if so
                if (event.getAction() == MotionEvent.ACTION_MOVE) {
                    hyp = (float) Math.sqrt((dX*dX)+(dY*dY));
                    angle = (float) Math.atan(Math.abs(dY/dX));

                    if (hyp > radius) {
                        //if dX is positive (bmpBall is too far to right)
                        if (dX >= 0 ) {
                            x = zX + (radius* FloatMath.cos(angle));
                        }
                        else if (dX <= 0) {
                            x = zX - (radius* FloatMath.cos(angle));
                        }

                        if (dY >= 0) {
                            y = zY + (radius* FloatMath.sin(angle));
                        }
                        else if (dY <= 0) {
                            y = zY - (radius* FloatMath.sin(angle));
                        }
                    }
                }
                // Reset bmp ball to center when it is let go,
                // Set  x and y to 0 as the default co-ords will then be used
                else if (event.getAction() == MotionEvent.ACTION_UP) {
                    // TODO gradually move ball to center
                    x = y = 0;
                    dX = dY = 0;
                }
                return true;
            }
        });

        gameLoopThread = new GameLoopThread(this);
        holder = getHolder();
        holder.addCallback(new SurfaceHolder.Callback() {
            @Override
            public void surfaceDestroyed(SurfaceHolder holder) {
                boolean retry = true;
                gameLoopThread.setRunning(false);
                while (retry) {
                    try {
                        gameLoopThread.join();
                        retry = false;
                    } catch (InterruptedException e) {
                    }
                }
            }

            @Override
            public void surfaceCreated(SurfaceHolder holder) {
                gameLoopThread.setRunning(true);
                gameLoopThread.start();
            }

            @Override
            public void surfaceChanged(SurfaceHolder holder, int format,
                                       int width, int height) {
            }
        });
        bmpBall = BitmapFactory.decodeResource(getResources(), R.drawable.ball);
        bmpBall = Bitmap.createScaledBitmap(bmpBall, 600, 600, true);

        bmpBallBG = BitmapFactory.decodeResource(getResources(), R.drawable.ball_bg);
        bmpBallBG = Bitmap.createScaledBitmap(bmpBallBG, 900, 900, true);
    }

    /**
     * Method that focusing on updating parts of the activity that aren't
     * focused on drawing. Makes sure a connection is kept alive between
     * the server and this particular client
     */
    protected void update() {
        if (connection.isConnected) {
            move.setStrMove(dX, dY);
            connection.sendMove(move);
        }
        else {      //attempt to reconnect
            connection.setupSocket();
        }
    }

    @Override
    protected void onDraw(Canvas canvas) {

        zX = canvas.getWidth()/2;
        zY = canvas.getHeight()/2;


        canvas.drawColor(Color.GREEN);

        canvas.drawBitmap(bmpBallBG, zX - bmpBallBG.getWidth()/2, zY - bmpBallBG.getHeight()/2, null);

        // Draw ball in center of thumbstick (center of canvas), when activity starts
        if (x == 0 && y == 0) {
            canvas.drawBitmap(bmpBall, zX - bmpBall.getWidth()/2, zY - bmpBall.getHeight()/2, null);
        }
        else {
            canvas.drawBitmap(bmpBall, x-bmpBall.getWidth()/2, y-bmpBall.getHeight()/2, null);
        }

    }
}


class GameLoopThread extends Thread {
    private MoveControllerView view;
    private boolean running = false;

    public GameLoopThread(MoveControllerView view) {
        this.view = view;
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
                    view.onDraw(c);
                }
            } finally {
                if (c != null) {
                    view.getHolder().unlockCanvasAndPost(c);
                }
            }
        }
    }
}
