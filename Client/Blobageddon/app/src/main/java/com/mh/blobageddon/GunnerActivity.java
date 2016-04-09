package com.mh.blobageddon;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;

public class GunnerActivity extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gunner);


        setContentView(new GunnerView(this));
    }

}
