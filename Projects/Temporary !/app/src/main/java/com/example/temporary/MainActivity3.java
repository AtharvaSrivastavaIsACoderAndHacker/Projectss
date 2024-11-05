package com.example.temporary;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.os.IResultReceiver;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

public class MainActivity3 extends AppCompatActivity {
    ListView lisst;
    String[] arr = {"Click any text","FOR","ReclyclerView","Hello", "Hi", "You","Are A Gaay !","Heoooooo", "Hit", "Your"," Mad","Hamara List View","ScrollView Do Mujhe"};
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main3);


        lisst = findViewById(R.id.list);
//        Default Android Adapter
//        ArrayAdapter<String> ad;
//        ad = new ArrayAdapter(this, android.R.layout.simple_list_item_1, arr);
        Adapterr ad = new Adapterr(this, R.layout.my_layout , arr);
        lisst.setAdapter(ad);
//        lisst.setOnItemClickListener(new AdapterView.OnItemClickListener() {
//            @Override
//            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
//                Toast.makeText(MainActivity3.this, arr[position], Toast.LENGTH_SHORT).show();
//            }
//        });

    }
    public void four (View v){
        Intent intentt = new Intent(this, MainActivity4.class);
        startActivity(intentt);
    }
}