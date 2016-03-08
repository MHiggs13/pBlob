//package com.mh.blobageddon;
//
//import java.io.DataOutputStream;
//import java.io.IOException;
//import java.net.InetAddress;
//import java.net.Socket;
//import java.net.UnknownHostException;
//import android.os.Handler;
//
///**
// * Created by michaelh on 24/11/2015.
// */
//public class Client extends Thread{
//
//    private Socket sock = null;
//    private String msg = "";
//    private boolean running = true;
//    private Handler clientHandler;
//
//    public Client() {
//    }
//
//    public Client(Handler clientHandler) {
//        this.clientHandler = clientHandler;
//    }
//
//    public void setMsg(String msg) {
//        this.msg = msg;
//    }
//
//    public void setRunning (boolean running) {
//        //allows running to be set to false so thread will end
//        this.running = running;
//    }
//
//    public boolean getConnected() {
//        // TODO change to a better way to check what to return
//        if (sock == null) {
//            return false;
//        }
//        return sock.isConnected();
//    }
//
//    @Override
//    public void run() {
//        //connect to python server
//        connectToServer();
//        //loop while functionality between client and server is being carried out
//        while (running) {
//            //if the button has been clicked in mainActivity send message
//            MainActivity.semSendMessage.acquireUninterruptibly();
//            sendString();
//        }
//
//    }
//
//    public void connectToServer() {
//        // Only connect if not connected already
//        if ( sock == null || !sock.isConnected()) {
//            try {
//                //address and port number of machine that server is running on
//                //Belfast IP
//                InetAddress addr = InetAddress.getByName("192.168.0.15");
//                //Home IP
//                //InetAddress addr = InetAddress.getByName("192.168.1.102");
//                int portNum = 8313;
//
//                //create socket for connecting to server with servers address and port number
//                sock = new Socket(addr, portNum);
//            } catch (UnknownHostException e) {
//                //catch exceptions to do with connecting to server
//                e.printStackTrace();
//            } catch (Exception e) {
//                //general catch all exception
//                e.printStackTrace();
//            }
//        }
//        clientHandler.sendEmptyMessage(0);
//    }
//
//    private void sendString() {
//        try {
//            // create stream to allow data to be transfered to server using sock
//            DataOutputStream dOut = new DataOutputStream(sock.getOutputStream());
//
//            //send string in dOut to server, dOut.flush() does send and flushes dOut
//            dOut.writeUTF(msg);
//            dOut.flush();
//        }
//        catch (IOException e) {
//            //catch exceptions with the writer and readers
//            e.printStackTrace();
//        }
//        catch (Exception e) {
//            //general catch all exception
//            e.printStackTrace();
//        }
//    }
//}
