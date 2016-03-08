package com.mh.blobageddon;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Message;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;


import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Semaphore;
import android.os.Handler;
import java.util.logging.LogRecord;

public class MainActivity extends ActionBarActivity {

    private Socket sock = new Socket();
    private boolean connected = false;
    private Connection connection;
    //private Bitmap ball;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        connection = Helper.conn;

        updateUi();
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
            try {
                connected = new SendMsgTask().execute(msg).get();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
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

        Intent intent = new Intent(this, MoveControllerActivity.class);

        Bundle b = new Bundle();
        b.putInt("key", 1); //Your id
        intent.putExtras(b); //Put your id to your next Intent
        startActivity(intent);
        finish();

        startActivity(intent);

    }

    public void btnTestViewClicked(View view) {

        Intent intent = new Intent(this, TestAtivity.class);
        startActivity(intent);
    }

    private class ConnectTask extends AsyncTask<Void, Void, Socket>
    {
        Socket sock;

        public Socket getSock() {
            return sock;
        }

        protected Socket doInBackground(Void... params) {
            try {
                System.out.println("@@@IN CONNECT TASK");
                //address and port number of machine that server is running on
                //Belfast IP
                //InetAddress addr = InetAddress.getByName("192.168.0.15");
                //Home IP
                //InetAddress addr = InetAddress.getByName("192.168.1.102");
                // QUBSec IP
                //InetAddress addr = InetAddress.getByName("143.117.228.31");
                //192.168.42.20
                InetAddress addr = InetAddress.getByName("192.168.42.20");

                int portNum = 8313;

                //create socket for connecting to server with servers address and port number
                sock = new Socket(addr, portNum);
            } catch (UnknownHostException e) {
                //catch exceptions to do with connecting to server
                e.printStackTrace();
            } catch (Exception e) {
                //general catch all exception
                e.printStackTrace();
            }
            return sock;
        }
    }

    private class SendMsgTask extends AsyncTask<String, Void, Boolean> {

        protected Boolean doInBackground(String... arrMsg) {
            String msg = arrMsg[0];
            try {
                // create stream to allow data to be transfered to server using sock
                DataOutputStream dOut = new DataOutputStream(sock.getOutputStream());

                //send string in dOut to server, dOut.flush() does send and flushes dOut
                dOut.writeUTF(msg);
                dOut.flush();
                return Boolean.TRUE;
            }
            catch (IOException e) {
                //catch exceptions with the writer and readers
                e.printStackTrace();
                return Boolean.FALSE;
            }
            catch (Exception e) {
                //general catch all exception
                e.printStackTrace();
                return Boolean.FALSE;
            }
        }
    }
}