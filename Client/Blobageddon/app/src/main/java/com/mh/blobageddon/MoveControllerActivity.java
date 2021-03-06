package com.mh.blobageddon;

import android.app.Activity;
import android.os.Bundle;

public class MoveControllerActivity extends Activity {

    private Connection connection = Helper.conn;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_move_controller);

        /* Busy wait loop, GState.GAME_SCREEN must be sent to server,
        if that happens then display the new view. Note condition will
        return true even if the message is sent but not received. */
        while (!(connection.sendStateChange(com.mh.blobageddon.GState.GAME_SCREEN)));

        setContentView(new MoveControllerView(this));
    }

    protected void onStart() {
        super.onStart();
    }

}
