questions = {
  "q1" : ["q-1v","q-1a","q-1r"],
  "q2" : ["q-2v","q-2a","q-2r"],
  "q3" : ["q-3v","q-3a","q-3r"],
  "q4" : ["q-4v","q-4a","q-4r"],
  "q5" : ["q-5v","q-5a","q-5r"],
}
background_color = {
  'v' : 'v_box',
  'a' : 'a_box',
  'r' : 'r_box',

}
function myFunction(question, answer, color)
{
    var answers = questions[question];
    // the array of whichever question you are in the the dict: questions

    for(var i = 0; i < answers.length; i++){
      if (answers[i]==answer){
        //if selected
        document.getElementById(answers[i]).classList.add("selected");
        // document.getElementById(answers[i]).classList.remove(background_color[color]);
        console.log("Selected " + answers[i]);
      }

      else{
        // document.getElementById(answers[i]).classList.add(background_color[color]);
        document.getElementById(answers[i]).classList.remove("selected");
        console.log("Unselected " + answers[i]);
      }

    }
  }
