package com.mh.blobageddon;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.view.View;
import android.view.Window;

public class TestAtivity extends ActionBarActivity {

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_test_ativity);
        //requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(new GunnerView(this));
    }
}
