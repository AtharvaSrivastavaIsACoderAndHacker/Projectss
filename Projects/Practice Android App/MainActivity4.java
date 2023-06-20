package com.example.temporary;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;

public class MainActivity4 extends AppCompatActivity {

RecyclerView rv = findViewById(R.id.rv);
String[] arre = {"Hello", "Hi", "You","Are A Gaay !","Heoooooo", "Hit", "Your"," Mad","Hamara List View","ScrollView Do Mujhe"};


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main4);

        rv.setLayoutManager(new LinearLayoutManager(this));
        CustomAdapter c = new CustomAdapter(arre);
        rv.setAdapter(c);
    }
}