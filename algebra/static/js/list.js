'use strict';

const MQ = MathQuill.getInterface(2);
const messenger = new Messenger();
let forms = [];

function makeForm( link, empty=false )
{
    $("#expression-list a").removeClass('active');
    $( link ).addClass('active');

    let id = $( link ).attr('id').split('-')[2];

    let expression = {}
    if (empty)
      expression = { expression:'', expression_type:'EQ', level:1, solution:''}
    else expression = messenger.expressions[id];

    let $form = $(`
      <form id='js-expr-form-${id}' class='expression-form' onsubmit='event.preventDefault(); submitForm(this);'>
          <div class='form-group'>
              <label for'expression'>Expression</label>
              <input type='text' name='expression' class='form-control'
               value='${expression.expression}' required>
          </div>
          <div class='form-group'>
              <label for'solution'>Solution</label>
              <input type='text' name='solution' class='form-control'
               value='${expression.solution}' required>
          </div>
          <div class='form-group'>
              <label for'solution'>Type</label>
              <select name='type' class='form-control'>
                  <option value="Equation" ${expression.expression_type == "EQ" ? "selected" : ""}>Equation</option>
                  <option value="Inequation" ${expression.expression_type == "IN" ? "selected" : ""}>Inequation</option>
                  <option value="EquationSystem" ${expression.expression_type == "ES" ? "selected" : ""}>Equation System</option>
              </select>
          </div>
          <div class='form-group'>
              <label for'level'>Level</label>
              <input type='text' name='level' class='form-control'
               value='${expression.level}' required>
          </div>

          <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    `);

    $("#expression-form form").remove();
    $("#expression-form #expression-form-placeholder").remove();
    $("#expression-form").prepend($form);
}

function submitForm( form )
{
    let $form = $( form );
    let formId = $form.attr('id').split('-');
    let url = "/algebra/api/expression"

    if (formId.length == 4) // modification
    { url += "/" + formId[3]; }

    let expression = $('input[name="expression"]', $form).val();
    let solution = $('input[name="solution"]', $form).val();
    let level = $('input[name="level"]', $form).val();
    let type = $('select[name="type"]', $form).val();

    $.ajax({
        url: url,
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            expression: expression,
            solution: solution,
            level: level,
            type: type
        })
    }).done( (x) => {
        console.log("SUCCESS: " + x);
        $("#expression-form button").removeClass("btn-primary");
        $("#expression-form button").removeClass("btn-danger");
        $("#expression-form button").addClass("btn-success");
    }).fail( (xhr) => {
      console.log("ERROR: " + xhr.responseText);
      $("#expression-form button").removeClass("btn-primary");
      $("#expression-form button").removeClass("btn-success");
      $("#expression-form button").addClass("btn-danger");
    });
}

$(document).ready( () => {
    messenger.fetch().then( function(data)
    {
        let $dom = $( '#expression-list' );
        messenger.expressions.forEach( function( e )
        {
            $dom.append($(`
              <a class='list-group-item' id='js-expr-${e.id}' onclick='makeForm(this)'>
                <div class="mq-algebra-expression">${e.expression}</div>
              </a>`
            ));
        });

        // MathQuill rendering
        let expressions = document.getElementsByClassName("mq-algebra-expression");
        console.log(expressions);
        for (let expression of expressions)
        { MQ.StaticMath(expression); }

    }).catch( console.log );
});
