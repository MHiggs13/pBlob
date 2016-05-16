package com.mh.blobageddon;
import android.os.AsyncTask;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;
import java.util.Enumeration;
import java.util.concurrent.ExecutionException;

/**
 * Created by michaelh on 24/02/2016.
 */
public class Connection extends Thread{

    private Socket sock = new Socket();
    public boolean isConnected = false;

    private boolean isDoingReceive = false;

    ////////////////////////////////////////
    //Activity Variables
    ////////////////////////////////////////
    private GState state;
    private int numTeams = -1;
    private boolean isDriver = false;
    private String msg = "";

    public Connection() {
        state = GState.MAIN_SCREEN;
        setupSocket();
        kickStartConnection();
    }

    public void kickStartConnection() {
        if (!isConnected) {
            setupSocket();
        }
        if (isConnected) {
            start();
        }
    }
    public GState getGState() {
        return state;
    }

    public void setGState(GState state) {
        this.state = state;
    }

    public int getNumTeams() {
        return numTeams;
    }

    public boolean getIsDriver() {
        return isDriver;
    }

    public String getAddress() {

        return sock.getLocalSocketAddress().toString();
    }

    @Override
    public void run() {
        while (!isConnected) {
            setupSocket();
        }
        while (isConnected){
            msg = receiveMsg();
            if (getGState().equals(GState.TEAM_SCREEN) && getNumTeams() == -1) {
                sendAwake();
            }
        }

    }

    public void setupSocket() {
        try {
            sock = new ConnectTask().execute().get();
            if (sock!= null && sock.isConnected()) {
                try {
                    sock.getInputStream(); // will fail if disconnection
                    isConnected = true;
                } catch (IOException e) {
                    isConnected = false;
                    System.out.print(isConnected);
                    e.printStackTrace();
                }
            }
            else {
                isConnected = false;
            }
        }
        catch (Exception e) {
            sock = null;
            e.printStackTrace();
        }
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
    public boolean sendAwake() {
        boolean isSent = false;
        try {
            isSent =  new SendMsgTask().execute("AW:"+getGState()+":").get();
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
            isSent=  new SendMsgTask().execute("DR:"+move.getStrMove()+":").get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        finally {
            return isSent;
        }
    }

    /** Send the amount of fires pressed by the user, followed by a comma and then the angle the
     * client wants the gun to turn to.
     *
     * @param str fireTally + "," + angle
     * @return
     */
    public boolean sendGun(String str) {
        // todo may need to check isConnected
        boolean isSent = false;
        try {
            isSent=  new SendMsgTask().execute("GU:" + str + ":").get();
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
     * Send a GState to the server to change the server's GState/view,
     * the client's activity is changed after the GState change
     * is successfully sent to the server.
     *
     * @param state an enum that signifies the "GState" the server should be in
     * @return returns true if message succesfully sent to server
     */
    public boolean sendStateChange(GState state) {
        // todo may need to check isConnected
        boolean isSent = false;
        try {
            isSent =  new SendMsgTask().execute("SC:"+state.toString()+":").get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        finally {
            return isSent;
        }
    }


    /**Receive a GState change from the server. The server will only send a GState change when a
     * change is necessary. The socket.read() will timeout after a delay of 100ms, meaning this
     * method can be called repeatedly and not slow the client too much.
     *
     *
     * @return the current GState of the connection
     */
    public GState receiveStateChange() {
        // todo may need to check isConnected
        if (!isDoingReceive) {
            new ReceiveStateTask().execute();
        }
        return state;
    }

    /** Receive a message from the server. This uses the ReceiveMsg AsyncTask. This method is
     * primarily used by TeamSelectionActivity, to receive information about team orderings.
     *
     * @return String of the message sent from the server, or if no message sent the empty String
     */
    public String receiveMsg() {
        String msg = "";
        if (!isDoingReceive) {
            try {
                msg =  new ReceiveMsgTask().execute().get();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            } finally {
                if (!msg.equals("")) {

                }
                return msg;
            }
        }
        else {
            return msg;
        }
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
                InetAddress addr = InetAddress.getByName("192.168.0.18");
                //Home IP
//                InetAddress addr = InetAddress.getByName("192.168.1.102");
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
            System.out.println("SEND: " + msg);
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

    /** Receives a byte array from the Server, converts byte array to a string, then checks if the
     * String received was in relation to a stateChange. If it was change the GState.
     *
     */
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

            if (!msg.equals(state.toString())) { //if GState sent does not equal current GState change GState
                if (msg.equals(GState.MAIN_SCREEN.toString())) { // todo ifs added for safety, a direct conversion GState = msg might be possible
                    state = GState.MAIN_SCREEN;
                }
                else if (msg.equals(GState.GAME_SCREEN.toString())) {
                    state = GState.GAME_SCREEN;
                }
                else if (msg.equals(GState.TEAM_SCREEN.toString())) {
                    state = GState.TEAM_SCREEN;
                }
            }
            isDoingReceive = false;
            return null;
        }
    }

    /** Receives a byte array from the Server, converts byte array to string and returns String
     *
     */
    private class ReceiveMsgTask extends AsyncTask<Void, Void, String>
    {
        protected String doInBackground(Void... params) {
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
                if (!msg.equals(""))
                    System.out.println("MSG: " + msg);
                String[] parts = msg.split(":");

                // message is about a state change
                if (parts.length > 0) {
                    if (parts[0].equals("SC")) {
                        if (parts[1].equals(GState.TEAM_SCREEN.toString())) {
                            setGState(GState.TEAM_SCREEN);
                        } else if (parts[1].equals((GState.GAME_SCREEN.toString()))) {
                            System.out.println("part[2]: " + parts[parts.length-1]);
                            setGState((GState.GAME_SCREEN));
                            if (parts[2].equals("driver")) {
                                isDriver = true;
                            }
                            else {
                                isDriver = false;
                            }
                        }
                        else if (parts[1].equals((GState.MAIN_SCREEN.toString()))) {
                            setGState((GState.MAIN_SCREEN));
                        }
                    }
                    // message is about the number of teams playing
                    else if (parts[0].equals("NT")) {
                        numTeams = Integer.parseInt(parts[1]);
                    }
                }

            } catch (SocketTimeoutException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            isDoingReceive = false;
            return msg;
        }
    }
}
