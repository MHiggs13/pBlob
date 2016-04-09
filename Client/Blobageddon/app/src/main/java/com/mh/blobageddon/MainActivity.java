package com.mh.blobageddon;

import android.content.Intent;
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

    private Socket sock = new Socket();
    private boolean connected = false;
    private Connection connection;
    private StateUpdate receiveStateT;
    private boolean isClicked = false;
    //private Bitmap ball;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        connection = Helper.conn;

        updateUi();
    }

    @Override
    protected void  onStart() {
        super.onStart();
        // todo is this necessary
        if (connection.isConnected == false) {
            connection.setupSocket();
        }

        receiveStateT = new StateUpdate();
        receiveStateT.start();
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
        CheckBox reconnectCkBx = (CheckBox)findViewById(R.id.connectedCkBx);
        Button reconenctBtn = (Button) findViewById(R.id.reconnectBtn);
        if (!connected) {
            // If client is not connected, uncheck checkbox and make button viewable
            reconnectCkBx.setChecked(false);
            reconenctBtn.setVisibility(View.VISIBLE);
        }
        else {
            // If client is conencted check checkbox and make button invisible
            reconnectCkBx.setChecked(true);
            reconenctBtn.setVisibility(View.INVISIBLE);
        }
    }

    public void btnSendTextToServerClicked(View view) {
        // send string entered into etxMsg to server, so it can display
        EditText etxMsg = (EditText) findViewById(R.id.etxMsg);
        String msg = etxMsg.getText().toString();

//        // send message to Client object so it can be sent to server
//        client.setMsg(msg);
//
//        // up the semaphore to allow client to send
//        semSendMessage.release();
        if (connected) {
            connected = connection.sendMessage(msg);
        }
        updateUi();
    }

    public void btnReconnectClicked(View view) {
        // Method to allow the user to reconnect if they lose their connection to server
        if (!connected) {
            connection.setupSocket();
        }
        updateUi();
    }

    public void btnMoveControllerActivityClicked(View view) {
        changeMoveActivity();
    }

    public void changeMoveActivity() {
        isClicked = true;
        Intent intent = new Intent(this, MoveControllerActivity.class);

        Bundle b = new Bundle();
        b.putInt("key", 1); // Your id
        intent.putExtras(b); // Put your id to your next Intent
        startActivity(intent);
        finish();

        startActivity(intent);
    }

    public void changeGunnerActivity() {

        System.out.println("GUNNER STARTED");
        isClicked = true;
        Intent intent = new Intent(this, GunnerActivity.class);

        startActivity(intent);
        finish();

        startActivity(intent);
    }


    public void btnTestViewClicked(View view) {

        Intent intent = new Intent(this, TestAtivity.class);
        startActivity(intent);
    }

    private class StateUpdate extends Thread {
        /* Thread checks every 0.1s if a state change has occurred, if state change has occured. Move
       to the appropriate activity.
       */
        @Override
        public void run() {
            while (connection.getState() == com.mh.blobageddon.State.MAIN_SCREEN && !isClicked) {
                connection.receiveStateChange();

                try {
                    this.sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                // if current state is not main screen, change activity to appropriate
                if (connection.getState() != com.mh.blobageddon.State.MAIN_SCREEN && !isClicked) {
                    if (connection.getState() == com.mh.blobageddon.State.GAME_SCREEN) {
                        System.out.println("GAMESCREEN SHOULD APPEAR");
                        changeGunnerActivity();
                    }
                }
            }
            System.out.println("OUT OF LOOP, THREAD DEAD");
            try {
                this.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}