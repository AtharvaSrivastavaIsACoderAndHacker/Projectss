package com.example.temporary;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    public static final String EXTRA_NAME = "com.example.temporary.extra.NAME";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }






        public void oneTOtwo (View v){
            EditText EmailAdd = findViewById(R.id.address);
            EditText EmailSub = findViewById(R.id.subject2);
            EditText textt = findViewById(R.id.emailText);

            String add1 = EmailAdd.getText().toString();
            String subject = EmailAdd.getText().toString();
            String [] addresses = {add1};
            String text = textt.getText().toString();

            Intent intent2 = new Intent(Intent.ACTION_SEND);
            intent2.setType("*/*");
            intent2.putExtra(Intent.EXTRA_EMAIL, addresses);
            intent2.putExtra(Intent.EXTRA_SUBJECT, subject);
            intent2.putExtra(Intent.EXTRA_TEXT, text);
            if(intent2.resolveActivity(getPackageManager()) != null){
                Toast.makeText(this, "Choose Your Preffered Email Sending App !  ", Toast.LENGTH_SHORT).show();
                startActivity(intent2);
            }

        }
    public void go (View v){
        Intent intent = new Intent(this, MainActivity2.class);
        startActivity(intent);
    }


}
