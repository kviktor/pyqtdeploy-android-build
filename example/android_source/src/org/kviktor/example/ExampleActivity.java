package org.kviktor.example;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.graphics.Color;
import android.os.Build;
import android.util.Log;

import org.json.JSONObject;
import org.json.JSONException;


public class ExampleActivity extends org.qtproject.qt5.android.bindings.QtActivity
{
    private static final String TAG = "ExampleActivity";
    private static final String CHANNEL_ID = "my_channel";

    private static ExampleActivity m_instance;
    private static NotificationManager m_notificationManager;


    public ExampleActivity()
    {
        Log.i(TAG, "ExampleActivity ctor");
        m_instance = this;
    }

    public static String sendNotification(String data) {
        Log.i(TAG, "sendNotification called with " + data);

        String title;
        String text;

        try {
            JSONObject jsonData = new JSONObject(data);
            title = jsonData.getString("title");
            text = jsonData.getString("text");
        } catch(JSONException e) {
            Log.e(TAG, "Exception during JSON", e);
            title = "error";
            text = "text";
        }

        if(m_notificationManager == null) {
            m_notificationManager = (NotificationManager)m_instance.getSystemService(Context.NOTIFICATION_SERVICE);

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                int importance = NotificationManager.IMPORTANCE_DEFAULT;
                NotificationChannel m_channel = new NotificationChannel(CHANNEL_ID, "channel name", importance);

                m_channel.setDescription("channel description");
                m_channel.enableLights(true);
                m_channel.setLightColor(Color.RED);
                m_channel.enableVibration(true);
                m_channel.setVibrationPattern(new long[]{100, 200, 300, 400, 500, 400, 300, 200, 400});

                m_notificationManager.createNotificationChannel(m_channel);
            }
        }

        Notification notification = new Notification.Builder(m_instance, CHANNEL_ID)
            .setContentTitle(title)
            .setContentText(text)
            .setSmallIcon(R.mipmap.duck)
            .build();

        m_notificationManager.notify(1, notification);

        Log.i(TAG, "sendNotification finished");

        try {
            return new JSONObject().put("success", true).toString();
        } catch(JSONException e) {
            // should really not happen
            return "{}";
        }
    }
}
