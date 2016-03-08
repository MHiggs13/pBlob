package com.mh.blobageddon;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

/**
 * Class that allows particular strings about player movement to be sent to the server.
 * Regex is used to make sure a string fits the required format for sending information
 * about the position of the thumb stick. Returns the string passed in for a valid Move
 * or returns an empty string for an invalid Move
 *
 * @Param strMove The vetted string that decribes the position of the thumbstick
 *                  must be of the format "*float*, *float*;".
 *
 * Created by michaelh on 24/02/2016.
 */
public class Move {

    private String strMove;
    private String strPatttern = "(^-?[0-9]\\d*(\\.\\d+)?\\,\\ -?[0-9]\\d*(\\.\\d+)?;$)";

    Pattern p =  Pattern.compile(strPatttern);

    public Move(float x, float y) {
        setStrMove(x, y);
    }

    public String getStrMove() {
        return strMove;
    }
    public void setStrMove(float x, float y) {
        String str = x + ", " + y + ";";
        this.strMove = vetStrMove(str);
    }


    /* Vet the string and make sure it follows the format "dX, dY;"
       Return string if valid, return empty string if not */
    private String vetStrMove(String strMove) {
        Matcher m = p.matcher(strMove);

        if (m.find()) {
            return strMove;
        }
        else {
            return "";
        }
    }
}
