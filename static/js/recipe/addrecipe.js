document.addEventListener('DOMContentLoaded', function() {
    var addInstructionBtn = document.getElementById('add_instruction');
    var instructionList = document.getElementById('instruction_list');
    var count = 1;
  
    addInstructionBtn.addEventListener('click', function() {
      var instructionInput = document.createElement('input');
      instructionInput.type = 'text';
      instructionInput.className = 'form-control';
      instructionInput.name = 'instruction_' + (++count);
      instructionInput.required = true;
  
      var instructionItem = document.createElement('li');
      instructionItem.appendChild(instructionInput);
  
      instructionList.appendChild(instructionItem);
    });
  });
  