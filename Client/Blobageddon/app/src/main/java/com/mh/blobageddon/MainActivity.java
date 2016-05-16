package com.mh.blobageddon;

import android.content.Intent;
import android.graphics.Canvas;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

import java.net.Socket;

public class MainActivity extends ActionBarActivity {
    private Connection connection;
    private MainUpdate mainUpdate = new MainUpdate();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        connection = Helper.conn;

        /* todo may need moved to another place. Needs a place where halting thread can be stopped
           when app closed and then restarted onStart()
        */
        mainUpdate.start();

        updateUi();
    }

    @Override
    protected void  onStart() {
        super.onStart();
    }

    @Override
    protected void onStop() {
        super.onStop();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        // noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    public void updateUi() {
        EditText connectionLbl = (EditText) findViewById(R.id.connectionLbl);
        Button teamSelectBtn = (Button) findViewById(R.id.btnTeamSelection);
        EditText ipLbl = (EditText) findViewById(R.id.ipLbl);
        if (!connection.isConnected) {
            // If client is not connected, updated the connection message and change the button text
            connectionLbl.setText("You are NOT connected.");
            teamSelectBtn.setText("Reconnect");
            ipLbl.setText("IP: _._._._");
        }
        else {
            // If client is  connected, updated the connection message and change the button text
            connectionLbl.setText("You are connected.");
            teamSelectBtn.setText("Select Team");
            String address = connection.getAddress();
            if (!address.equals("")) {
                ipLbl.setText("IP:" + connection.getAddress());
            }
        }
    }

    public void btnTeamSelectionClicked(View view) {
        Button teamSelectBtn = (Button) findViewById(R.id.btnTeamSelection);
        if (teamSelectBtn.getText().equals("Select Team")) {
            connection.sendStateChange(GState.TEAM_SCREEN);
        }
        else {
            connection.kickStartConnection();
        }
    }

    public void btnMoveControllerActivityClicked(View view) {
        changeMoveActivity();
    }

    public void changeMoveActivity() {
        Intent intent = new Intent(this, MoveControllerActivity.class);

        Bundle b = new Bundle();
        b.putInt("key", 1); // Your id
        intent.putExtras(b); // Put your id to your next Intent
        startActivity(intent);
        finish();

        startActivity(intent);
    }

    public void changeTeamSelectionActivity() {
        Intent intent = new Intent(this, TeamSelectionActivity.class);
        startActivity(intent);
    }

    public void changeGunnerActivity() {

        System.out.println("GUNNER STARTED");
        Intent intent = new Intent(this, GunnerActivity.class);

        startActivity(intent);
        finish();

        startActivity(intent);
    }


    public void btnTestViewClicked(View view) {

        Intent intent = new Intent(this, TestAtivity.class);
        startActivity(intent);
    }

    private class MainUpdate extends Thread {
        /* Thread checks every 0.1s if a state change has occurred, if state change has occurred. Move
       to the appropriate activity.
       */
        @Override
        public void run() {
            // busy wait loop that waits while the state says to stay on this screen
            while (connection.getGState() == GState.MAIN_SCREEN) {
                try {
                    this.sleep(100);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            updateUi();
                        }
                    });
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            if (connection.getGState() == GState.TEAM_SCREEN) {
                changeTeamSelectionActivity();
            }
        }
    }
}