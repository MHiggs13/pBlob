package com.mh.blobageddon;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.util.FloatMath;
import android.view.MotionEvent;

/**
 * Created by michaelh on 07/04/2016.
 */
public class Thumbstick {

    private Bitmap bmpBall, bmpBallBG;
    private float x, y, dX, dY, hyp, angle;
    private int zX, zY;

    public TouchRegion touchRegion;


    public Thumbstick(Context context) {
        bmpBall = BitmapFactory.decodeResource(context.getResources(), R.drawable.ball);
        bmpBall = Bitmap.createScaledBitmap(bmpBall, 600, 600, true);

        bmpBallBG = BitmapFactory.decodeResource(context.getResources(), R.drawable.ball_bg);
        bmpBallBG = Bitmap.createScaledBitmap(bmpBallBG, 900, 900, true);

        touchRegion = new TouchRegion(0, 0, bmpBallBG.getWidth(), bmpBallBG.getHeight());
    }

    public float getAngle() {
        return angle;
    }

    public void onMove(MotionEvent event, int id) {
        // Set dX and dY equal to distance away from center of screen
        final int index = event.findPointerIndex(id);
        x = event.getX(index);
        y = event.getY(index);

        dX = x - zX;
        dY = y - zY;

        int radius = bmpBall.getWidth() - 200;

        // Check if bmpBall goes out of bounds and fix if so
            hyp = (float) Math.sqrt((dX * dX) + (dY * dY));
            angle = (float) Math.atan(Math.abs(dY / dX));

            if (hyp > radius) {
                //if dX is positive (bmpBall is too far to right)
                if (dX >= 0) {
                    x = zX + (radius * FloatMath.cos(angle));
                } else if (dX <= 0) {
                    x = zX - (radius * FloatMath.cos(angle));
                }

                if (dY >= 0) {
                    y = zY + (radius * FloatMath.sin(angle));
                } else if (dY <= 0) {
                    y = zY - (radius * FloatMath.sin(angle));
                }
            }
            // convert to degrees to allow angle to be sent
            angle = (float) Math.toDegrees(angle);
            if (dX >= 0 && dY >= 0) {
                // angle is within 0-90
            } else if (dX >= 0) {
                // angle is within 270-360
                angle += 270;
            } else if (dY >= 0) {
                // angle is within 90-180
                angle += 90;
            } else {
                // angle is within 180-270
                angle += 180;
            }
    }

    public void onUp() {
        // TODO gradually move ball to center
        x = y = 0;
        dX = dY = 0;
        angle = -1;
    }

    public void onDraw(Canvas canvas) {
        zX = canvas.getWidth()/2;
        zY = (canvas.getHeight()/2)/2*3;

        touchRegion.setX(zX - bmpBallBG.getWidth()/2);
        touchRegion.setY(zY - bmpBallBG.getHeight()/2);

        canvas.drawColor(Color.CYAN);

        canvas.drawBitmap(bmpBallBG, touchRegion.getX(), touchRegion.getY(), null);
        // Draw ball in center of thumbstick (center of canvas), when activity starts
        if (x == 0 && y == 0) {
            canvas.drawBitmap(bmpBall, zX - bmpBall.getWidth()/2, zY - bmpBall.getHeight()/2, null);
        }
        else {
            canvas.drawBitmap(bmpBall, x-bmpBall.getWidth()/2, y-bmpBall.getHeight()/2, null);
        }
    }

}
