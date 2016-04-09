package com.mh.blobageddon;

/**
 * Created by michaelh on 07/04/2016.
 */
public class TouchRegion {

    private float x, y;
    private int width, height;


    public TouchRegion(float x, float y, int width, int height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    public boolean isXYIn(float x2, float y2) {
        return (x2 > x && x2 <x + width) && (y2 > y && y2 < y + height);
    }


    public float getX() {
        return x;
    }

    public void setX(float x) {
        this.x = x;
    }

    public float getY() {
        return y;
    }

    public void setY(float y) {
        this.y = y;
    }

    public int getWidth() {
        return width;
    }

    public void setWidth(int width) {
        this.width = width;
    }

    public int getHeight() {
        return height;
    }

    public void setHeight(int height) {
        this.height = height;
    }


}
