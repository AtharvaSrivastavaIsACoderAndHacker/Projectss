package com.example.meterometer;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.text.format.DateFormat;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);



//----------------------------------------------------------------------------------------------------------------------------------------



        Toast.makeText(this, "Welcome To MeterOMeter", Toast.LENGTH_SHORT).show();
        Button bumton = findViewById(R.id.button);
        TextView textv = findViewById(R.id.textView);
        EditText input = findViewById(R.id.editTextNumber);
        TextView date = findViewById(R.id.editTextDate);

        LocalDateTime ld = LocalDateTime.now();
        DateTimeFormatter df = DateTimeFormatter.ofPattern("dd/MM/yyyy  HH:mm");
        String MyDate = ld.format(df);
        date.setText("Date/Time -- "+MyDate);

        bumton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(MainActivity.this, "Conversion Complete !", Toast.LENGTH_SHORT).show();
                String s = input.getText().toString();
                if (s == "") {
                    Toast.makeText(MainActivity.this, "Pls Enter A Value !", Toast.LENGTH_SHORT).show();
                } else {
                    int kg = Integer.parseInt(s);
                    double pound = 2.205 * kg;
                    textv.setText("The Value In Pounds Is : " + pound);
                }
            }
        });





// ---------------------------------------------------------------------------------------------------------------------------------



    }
}