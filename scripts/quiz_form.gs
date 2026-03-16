/**
 * Google Apps Script: Quiz Form Generator (Verbose Logging Edition)
 */

const HARDCODED_CALLBACK = "https://webhook.site/93d40a6e-65b0-4249-ae92-87a756c50df9";

function doPost(e) {
  console.log("--- START DOPOST ---");
  try {
    console.log("Raw postData: " + e.postData.contents);
    var data = JSON.parse(e.postData.contents);
    var action = data.action || "create";
    console.log("Parsed action: " + action);

    if (action === "close") {
      return handleClose(data);
    }
    return handleCreate(data);
  } catch (err) {
    console.error("CRITICAL: doPost failed: " + err.toString());
    console.error("Stack: " + err.stack);
    return ContentService.createTextOutput(JSON.stringify({ error: err.toString() }))
                         .setMimeType(ContentService.MimeType.JSON);
  } finally {
    console.log("--- END DOPOST ---");
  }
}

function handleCreate(data) {
  console.log("ENTERING handleCreate");

  var formTitle = data.title || "Quiz";
  console.log("Creating form with title: " + formTitle);
  var form = FormApp.create(formTitle);
  var formId = form.getId();
  console.log("Form created. ID: " + formId);

  form.setIsQuiz(true);
  form.setCollectEmail(true);

  var questions = data.questions || [];
  console.log("Processing " + questions.length + " questions");

  for (var i = 0; i < questions.length; i++) {
    var q = questions[i];
    var item = form.addMultipleChoiceItem();
    item.setTitle(q.question);
    item.setPoints(1);

    var choices = [];
    var options = q.options || [];
    for (var j = 0; j < options.length; j++) {
      var isCorrect = (options[j] === q.correct_answer);
      choices.push(item.createChoice(options[j], isCorrect));
    }
    item.setChoices(choices);
    console.log("Added question " + (i+1) + ": " + q.question);
  }

  var finalCallback = data.callback_url || HARDCODED_CALLBACK;
  console.log("Setting callback URL: " + finalCallback);

  PropertiesService.getScriptProperties().setProperty("callback_" + formId, finalCallback);
  console.log("Property saved for key: callback_" + formId);

  console.log("Attempting to create installable trigger...");
  try {
    var trigger = ScriptApp.newTrigger("onFormSubmit")
      .forForm(form)
      .onFormSubmit()
      .create();
    console.log("Trigger created successfully. Trigger UID: " + trigger.getUniqueId());
  } catch (tErr) {
    console.error("TRIGGER CREATION FAILED: " + tErr.toString());
    throw tErr;
  }

  var response = {
    formUrl: form.getPublishedUrl(),
    formId: formId,
    callbackSet: finalCallback
  };
  console.log("Returning handleCreate response: " + JSON.stringify(response));

  return ContentService
    .createTextOutput(JSON.stringify(response))
    .setMimeType(ContentService.MimeType.JSON);
}

function handleClose(data) {
  console.log("ENTERING handleClose for ID: " + data.id);
  var formId = data.id;
  if (formId) {
    var form = FormApp.openById(formId);
    form.setAcceptingResponses(false);
    console.log("Form set to not accepting responses.");

    PropertiesService.getScriptProperties().deleteProperty("callback_" + formId);
    console.log("Property deleted for key: callback_" + formId);

    var triggers = ScriptApp.getProjectTriggers();
    console.log("Total project triggers found: " + triggers.length);
    for (var i = 0; i < triggers.length; i++) {
      if (triggers[i].getTriggerSourceId() === formId) {
        ScriptApp.deleteTrigger(triggers[i]);
        console.log("Deleted trigger for formId: " + formId);
      }
    }
  }
  return ContentService.createTextOutput(JSON.stringify({ status: "closed", id: formId }))
                       .setMimeType(ContentService.MimeType.JSON);
}

function onFormSubmit(e) {
  console.log("--- START ONFORMSUBMIT TRIGGER ---");
  try {
    var formResponse = e.response;
    var formId = e.source.getId();
    console.log("Trigger fired from Form ID: " + formId);

    var items = formResponse.getGradableItemResponses();
    var totalScore = 0;
    var maxScore = 0;

    for (var i = 0; i < items.length; i++) {
      totalScore += items[i].getScore();
      var item = items[i].getItem();
      if (item.getType() === FormApp.ItemType.MULTIPLE_CHOICE) {
        maxScore += item.asMultipleChoiceItem().getPoints();
      }
    }
    console.log("Calculated score: " + totalScore + "/" + maxScore);

    var callbackUrl = PropertiesService.getScriptProperties().getProperty("callback_" + formId) || HARDCODED_CALLBACK;
    console.log("Resolved callback URL: " + callbackUrl);

    var payload = {
      student_email: formResponse.getRespondentEmail(),
      score: totalScore,
      max_score: maxScore,
      form_id: formId,
      timestamp: formResponse.getTimestamp()
    };
    console.log("Payload prepared: " + JSON.stringify(payload));

    console.log("Executing UrlFetchApp...");
    var response = UrlFetchApp.fetch(callbackUrl, {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });

    console.log("HTTP Response Status: " + response.getResponseCode());
    console.log("HTTP Response Body: " + response.getContentText());
  } catch (err) {
    console.error("onFormSubmit CRITICAL FAILURE: " + err.toString());
    console.error("Stack: " + err.stack);
  } finally {
    console.log("--- END ONFORMSUBMIT TRIGGER ---");
  }
}