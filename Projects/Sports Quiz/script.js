const quesDB = [

    
      {  
        question: "Q1: Who Is Known As The Flying Fish In Sports World ?",
        a:"Michael Phelps",
        b:"Ryan Lochte",
        c:"Michael Andrine",
        d:"Nathan Adrian",
        ans: "ans1"
      },
      {  
        question: "Q2: What Is The National Game of England ?",
        a:"Rugby",
        b:"Tennis",
        c:"Football",
        d:"Cricket",
        ans: "ans4"
      },
      {  
        question: "Q3: Who Is Known As The Flying Sikh of India ?",
        a:"Mohinder Singh",
        b:"Ajit Pal Singh",
        c:"Milkha Singh",
        d:"Joginder Singh",
        ans: "ans3"
      },
      {  
        question: "Q4: Which Football Player Is Known A 'Black Pearl' ?",
        a:"Pele",
        b:"Usain Bolt",
        c:"Roosevelt",
        d:"Sachin Tendulkar",
        ans: "ans1"
      },
      {  
        question: "Q5: which Is The Largest Cricket Stadium of The World ?",
        a:"Eden Garden",
        b:"Narendra Modi Stadium Of Motera",
        c:"Lord's Stadium",
        d:"Melbourne Ground",
        ans: "ans2"
      },
      {  
        question: "Q6: Which National Cricket Team Is Called By 'Kangaroos' ?",
        a:"Indian Cricket Team",
        b:"Sri Lankan Cricket Team",
        c:"Austrailian Cricket Team",
        d:"South African Cricket Team",
        ans: "ans3"
      },
      {  
        question: "Q7: 'Playing It My Way' Is The Autobiography Of Which Sportsperson ?",
        a:"Sachin Tendulkar",
        b:"Usain Bolt",
        c:"PT Usha",
        d:"Muhammad Ali",
        ans: "ans1"
      },
      {  
        question: "Q8: Davis Cup Is Associated With Which Of The Following Game ?",
        a:"Cricket",
        b:"Hockey",
        c:"Badminton",
        d:"Lawn Tenis",
        ans: "ans4"
      }
]

let questionCount = 0;
let score = 0;

// definitions
const question = document.querySelector('.question');
const option1 = document.querySelector('#option1');
const option2 = document.querySelector('#option2');
const option3 = document.querySelector('#option3');
const option4 = document.querySelector('#option4');
const submit = document.querySelector('.submit');
const answers = document.querySelectorAll('.answer');

// functions
const loadQuestion = () => {
    const questionList = quesDB[questionCount];
    question.innerText = questionList.question;
    option1.innerText = questionList.a;
    option2.innerText = questionList.b;
    option3.innerText = questionList.c;
    option4.innerText = questionList.d;
}


loadQuestion();

const getCheckAsnwer = () => {
    let answer;

    answers.forEach((curAnsElem) => {
        if(curAnsElem.checked){
            answer = curAnsElem.id;
        }
    });
    return answer;
};




submit.addEventListener('click', () => {
    const checkedAnswer = getCheckAsnwer();
    // console.log(checkedAnswer);
    if(checkedAnswer === quesDB[questionCount].ans){
        score ++;
    }
    questionCount ++;

    if(questionCount < quesDB.length){
        loadQuestion();
    }
    else{}
});
 // abhi score add karna baki hai