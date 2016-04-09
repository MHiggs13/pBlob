package com.mh.blobageddon;

import android.animation.FloatArrayEvaluator;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.view.MotionEvent;

import java.util.Calendar;
import java.util.Date;

/**
 * Created by michaelh on 07/04/2016.
 */
public class FireButton {

    private Bitmap bmpButtonU, bmpButtonP;

    private float x, y, dX, dY;
    private int zX, zY;
    public TouchRegion touchRegion;
    private boolean isPressed = false;
    private int fireTally = 0;
    private int currSecond;

    public int getFireTally() {
        int tally = fireTally;
        fireTally = 0;
        return tally;
    }

    public FireButton(Context context) {
        bmpButtonU = BitmapFactory.decodeResource(context.getResources(), R.drawable.button_unpressed);
        bmpButtonU = Bitmap.createScaledBitmap(bmpButtonU, 900, 900, true);

        bmpButtonP = BitmapFactory.decodeResource(context.getResources(), R.drawable.button_pressed);
        bmpButtonP = Bitmap.createScaledBitmap(bmpButtonP, 900, 900, true);

        touchRegion = new TouchRegion(0, 0, bmpButtonU.getWidth(), bmpButtonU.getHeight());
        currSecond = Calendar.getInstance().get(Calendar.SECOND);

    }

    public void onDown() {
        isPressed = true;
        onUpdate();
    }

    public void onUp() {
        isPressed = false;
        onUpdate();
    }

    public void onDraw(Canvas canvas) {

        zX = canvas.getWidth() / 2;
        zY = canvas.getHeight() / 4;  // quarter of way down the screen

        touchRegion.setX(zX - bmpButtonU.getWidth() / 2);
        touchRegion.setY(zY - bmpButtonU.getHeight() / 2);

        if (!isPressed) {
            // draw unpressed bmp image
            canvas.drawBitmap(bmpButtonU, touchRegion.getX(), touchRegion.getY() , null);
        }
        else {
            // draw pressed bmp image
            canvas.drawBitmap(bmpButtonP, touchRegion.getX(), touchRegion.getY(), null);
        }
    }

    public void onUpdate() {

        if (isPressed &&  currSecond != Calendar.getInstance().get(Calendar.SECOND)) {
            fireTally ++;
            System.out.println("FIRE TALLY++");
            currSecond = Calendar.getInstance().get(Calendar.SECOND);
        }

    }
}
