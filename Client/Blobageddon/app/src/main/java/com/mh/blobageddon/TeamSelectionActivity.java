package com.mh.blobageddon;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

public class TeamSelectionActivity extends ActionBarActivity {

    private Connection connection;
    private int numTeams = -1;
    private TeamUpdate teamUpdate;
    private TextView[] arrTextViews;
    private Button[] arrButtons;
    private Button gameButton;
    private LinearLayout linearLayout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        linearLayout = new LinearLayout(this);
        linearLayout.setOrientation(LinearLayout.VERTICAL);
        linearLayout.setLayoutParams(new ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT));

        // Get a reference to the connection
        connection = Helper.conn;
        System.out.println("CurrState: " + connection.getGState());
        teamUpdate = new TeamUpdate();
        teamUpdate.start();

        setContentView(linearLayout);
    }

    @Override
    protected void  onStart() {
        super.onStart();
        // todo is this necessary
        if (connection.isConnected == false) {
            connection.setupSocket();
        }

        /* Receive total number of clients that are connected to the server, so that the correct
        number of team boxes can be created */
        // Busy wait loop, waiting to find out how many teams there are
        while (connection.getNumTeams() == -1);
        numTeams = connection.getNumTeams();

        arrTextViews = new TextView[numTeams];
        arrButtons = new Button[numTeams*2];

        for (int i = 0; i < numTeams;i++) {
            final int teamNumber = i;
            //create UI
            arrTextViews[i] = new TextView(this);
            arrTextViews[i].setText("Team " + (i + 1));
            linearLayout.addView(arrTextViews[i]);

            arrButtons[i * 2] = new Button(this);
            arrButtons[i * 2].setText("Be Driver");
            arrButtons[i * 2].setOnClickListener(new Button.OnClickListener() {
                public void onClick(View v) {
                    connection.sendMessage("RL:" + teamNumber + "driver:");
                }
            });
            linearLayout.addView(arrButtons[i * 2]);

            arrButtons[i * 2 + 1] = new Button(this);
            arrButtons[i * 2 + 1].setText("Be Gunner");
            arrButtons[i * 2 + 1].setOnClickListener(new Button.OnClickListener() {
                public void onClick(View v) {
                    connection.sendMessage("RL:" + teamNumber + "gunner:");
                }
            });
            linearLayout.addView(arrButtons[i * 2 + 1]);
        }

        gameButton = new Button(this);
        gameButton.setText("Start game");
        gameButton.setOnClickListener(new Button.OnClickListener() {
            public void onClick(View v) {
                connection.sendStateChange(GState.GAME_SCREEN);
            }
        });
        linearLayout.addView(gameButton);
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

    public void changeGunnerActivity() {

        System.out.println("GUNNER STARTED");
        Intent intent = new Intent(this, GunnerActivity.class);

        startActivity(intent);
        finish();

        startActivity(intent);
    }

    private class TeamUpdate extends Thread {
        /* Thread checks every 0.1s if a state change has occurred, if state change has occurred. Move
       to the appropriate activity.
       */
        @Override
        public void run() {
            while (connection.getGState() == GState.TEAM_SCREEN) {
                try {
                    this.sleep(100);
                    System.out.println("State:" + connection.getGState());
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            System.out.println("@@@@@@@@@@@@@@@@@@@@@");
            if (connection.getGState() == GState.GAME_SCREEN) {
                if (connection.getIsDriver()) {
                    changeMoveActivity();
                }
                else {
                    changeGunnerActivity();
                }
            }
            try {
                this.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
