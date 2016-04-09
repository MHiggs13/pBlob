package com.mh.blobageddon;

import android.os.AsyncTask;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;
import java.util.concurrent.ExecutionException;

/**
 * Created by michaelh on 24/02/2016.
 */
public class Connection {

    private Socket sock = new Socket();
    public boolean isConnected = false;
    private State state;
    private boolean isDoingReceive = false;

    public Connection() {
        state = State.MAIN_SCREEN;
        setupSocket();
    }

    public State getState() {
        return state;
    }

    public void setState(State state) {
        this.state = state;
    }

    public void setupSocket() {
        try {
            sock = new ConnectTask().execute().get();
            if (sock!= null && sock.isConnected()) {
                isConnected = true;
            }
        }
        catch (Exception e) {
            sock = null;
            e.printStackTrace();
        }
        System.out.println("SOCKET SETUP");
    }

    /**sends a String to the server, no special cases are required of the String for it to be sent
     * to the server.
     *
     * @param msg
     * @return true if message sent, false otherwise
     */
    public boolean sendMessage(String msg) {
        boolean isSent = false;
        try {
            isSent =  new SendMsgTask().execute(msg).get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        return isSent;
    }

    /**
     * Send a specific movement string that details the position
     * of the thumbstick. Return true if string sent successfully
     * and false if string not sent successfully
     * @param move vetted string to ensure the correct format for thumbstick position
     * @return
     */
    public boolean sendMove(Move move) {
        // todo may need to check isConnected
        boolean isSent = false;
        try {
            isSent=  new SendMsgTask().execute(move.getStrMove()).get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        finally {
            return isSent;
        }
    }

    /**
     * Send a State to the server to change the server's state/view,
     * the client's activity is changed after the state change
     * is successfully sent to the server.
     *
     * @param state an enum that signifies the "State" the server should be in
     * @return returns true if message succesfully sent to server
     */
    public boolean sendStateChange(State state) {
        // todo may need to check isConnected
        boolean isSent = false;
        try {
            isSent =  new SendMsgTask().execute(state.toString()).get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        finally {
            return isSent;
        }
    }


    /**Receive a state change from the server. The server will only send a state change when a
     * change is necessary. The socket.read() will timeout after a delay of 100ms, meaning this
     * method can be called repeatedly and not slow the client too much.
     * todo will cause a bit of lag at the minute but server will probably send regular updates to client
     *
     *
     * @return the current state of the connection
     */
    public State receiveStateChange() {
        // todo may need to check isConnected
        if (!isDoingReceive) {
            new ReceiveStateTask().execute();
        }
        System.out.println("STATE: "+ state);
        return state;
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
//                InetAddress addr = InetAddress.getByName("192.168.0.18");
                //Home IP
                InetAddress addr = InetAddress.getByName("192.168.1.102");
                // QUBSec IP
                //InetAddress addr = InetAddress.getByName("143.117.228.31");
                //192.168.42.20
                //InetAddress addr = InetAddress.getByName("192.168.42.20");

                int portNum = 8313;

                //create socket for connecting to server with servers address and port number
                sock = new Socket(addr, portNum);
                sock.setSoTimeout(1000);
            } catch (UnknownHostException e) {
                //catch exceptions to do with connecting to server
                e.printStackTrace();
            }catch (SocketException e) {
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
                // create stream to allow data to be transferred to server using sock
                DataOutputStream dOut = new DataOutputStream(sock.getOutputStream());

                //send string in dOut to server, dOut.flush() does send and flushes dOut
                dOut.writeBytes(msg);
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


    private class ReceiveStateTask extends AsyncTask<Void, Void, Void>
    {

        protected Void doInBackground(Void... params) {
            isDoingReceive = true;
            String msg = "";
            try {
                DataInputStream dIn = new DataInputStream(sock.getInputStream());
                int count = dIn.available();
                byte b[] = new byte[count];
                dIn.read(b);
                for (byte by:b) {
                    msg += (char) by;
                }
            } catch (SocketTimeoutException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

            if (!msg.equals(state.toString())) { //if state sent does not equal current state change state
                if (msg.equals(State.MAIN_SCREEN.toString())) { // todo ifs added for safety, a direct conversion state = msg might be possible
                    state = State.MAIN_SCREEN;
                }
                else if (msg.equals(State.GAME_SCREEN.toString())) {
                    state = State.GAME_SCREEN;
                }
            }
            isDoingReceive = false;
            return null;
        }
    }

}
