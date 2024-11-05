package com.example.temporary;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity2 extends AppCompatActivity {









    Button yes;
    Button no;
    TextView tv;
    private String[] questions = {
        "Java is a person ?","Java was introduced in 1233 ?","Java was created in c++ ?","Do java have abstract classes ?", "Does java supports interfaces ?","Thanks For Playing , Press Y Button 2 Times For Score !"
    };
    private boolean[] answers = {
            false,false,false,true,true, Boolean.parseBoolean(null)
    };
    private  int score = 0;
    private  int index = 0;









    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);

//==============================================================================================================================================
    yes = findViewById(R.id.yes);
    no = findViewById(R.id.button);
    tv = findViewById(R.id.textView);
    tv.setText(questions[index]);


        yes.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {



                if(index<=questions.length-1){
                            if(answers[index]){
                                score++;
                                Toast.makeText(MainActivity2.this, "Correct Answer !, Yayyyyy !!!!", Toast.LENGTH_SHORT).show();
                            }
                            else {
                                Toast.makeText(MainActivity2.this, "Wrong Answer !", Toast.LENGTH_SHORT).show();
                            }
                            index++;
                            if(index<=questions.length-1){
                                tv.setText(questions[index]);
                            }

                        }
                else {
                       if (score == questions.length-1){
                           Toast.makeText(MainActivity2.this, "Your Score Is "+score+", Congo It's Full Score !", Toast.LENGTH_SHORT).show();
                       }
                       else {
                           Toast.makeText(MainActivity2.this, "Your Score Is "+score, Toast.LENGTH_SHORT).show();
                       }
                }






                }
            });
            no.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {



                    if(index<=questions.length-1){
                        if(!answers[index]){
                            score++;
                            Toast.makeText(MainActivity2.this, "Correct Answer !, Yayyyyy !!!!", Toast.LENGTH_SHORT).show();
                        }
                        else {
                            Toast.makeText(MainActivity2.this, "Wrong Answer !", Toast.LENGTH_SHORT).show();
                        }
                        index++;
                        if(index<=questions.length-1){
                            tv.setText(questions[index]);
                        }

                    }
                    else {
                        if (score == questions.length-1){
                            Toast.makeText(MainActivity2.this, "Your Score Is "+score+", Congo It's Full Score !", Toast.LENGTH_SHORT).show();
                        }
                        else {
                            Toast.makeText(MainActivity2.this, "Your Score Is "+score, Toast.LENGTH_SHORT).show();
                        }
                    }





                }
            });

        }
        public void three (View v){
            Intent intentt = new Intent(this, MainActivity3.class);
            startActivity(intentt);
        }



//=============================================================================================================================================
    }
