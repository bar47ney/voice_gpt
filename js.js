import * as PlayHT from 'playht';
import fs from 'fs';

PlayHT.init({
  apiKey: '9f201cb006d84961806a7f56bd4b8621',
  userId: 'Sua0mbA64INLDYxzuIx4xmSDSnE2',
  defaultVoiceId: 's3://peregrine-voices/oliver_narrative2_parrot_saad/manifest.json',
  defaultVoiceEngine: 'PlayHT2.0',
});

// // Generate audio from text
// const generated = await PlayHT.generate('The options available will depend on the AI model that synthesize the selected voice. PlayHT API supports 3 different types of models. For all available options, see the typescript type definitions in the code.');

// // Grab the generated file URL
// const { audioUrl } = generated;

// console.log('The url for the audio file is', audioUrl);

const fileStream = fs.createWriteStream('turbo-playht.mp3');

// Stream audio from text
const stream = await PlayHT.stream('Hello Helen! I love you!', {
  voiceEngine: 'PlayHT2.0-turbo',
  voiceId: 's3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json',
  outputFormat: 'mp3',
  emotion: 'female_happy',
  styleGuidance: 10,
});

// Pipe stream into file
stream.pipe(fileStream);

// // клон голоса
// // Load an audio file
// const fileBlob = fs.readFileSync('voice-to-clone.mp3');

// // Clone the voice
// const clonedVoice = await PlayHT.clone('dolly', fileBlob, 'male');

// // Display the cloned voice information in the console
// console.log('Cloned voice info\n', JSON.stringify(clonedVoice, null, 2));

// // Use the cloned voice straight away to generate an audio file
// const fileStream = fs.createWriteStream('hello-dolly.mp3');
// const stream = await PlayHT.stream('Cloned voices sound realistic too.', {
//   voiceEngine: clonedVoice.voiceEngine,
//   voiceId: clonedVoice.id,
// });
// stream.pipe(fileStream);