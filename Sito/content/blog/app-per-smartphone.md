---
title: "App per smartphone"
date: 2022-05-09T11:18:56+06:00
featureImage: images/blog/blog-feature.jpg
tags: ["Tecnologia", "Android", "iPhone", "Apache", "Cordova"]
---
Tutti noi le usiamo quotidianamente, ma ci siamo mai chiesti come vengono create le app per smartphone? Vediamo quali sono i principali strumenti disponibili e quali sono le scelte tecniche alla base dell'app del Parco digitale della biodiversità umbra.

### Un mondo variegato (ma non troppo)

Le app per smartphone e tablet sono scritte con appositi linguaggi ed ambienti di programmazione, che consistono in una serie di programmi e librerie di funzioni già pronte. Ovviamente ogni grande categoria di smartphone ha il proprio ecosistema: 
    
- le app per **Android** sono scritte in Kotlin (fino a qualche tempo fa, in Java, che può essere ancora usato), ma possono anche essere scritte in C++;
- le app per **iPhone** sono scritte in Swift (fino a qualche tempo fa in Objective-C, che può essere ancora usato).      
    
Questi sono gli strumenti supportati direttamente dai grandi *player* del mercato degli smartphone, Alphabet (Google) ed Apple. Ovviamente sono del tutto incompatibili tra loro: un'app scritta per Android deve essere riscritta completamente per iPhone.

Per ovviare a questo problema sono nati una serie di strumenti che consentono di scrivere app per entrambe le grandi piattaforme senza dover duplicare il lavoro; lo scotto da pagare in questo caso sono le minori prestazioni (quasi sempre) ed un aggiornamento per forza di cose in ritardo rispetto agli strumenti supportati direttamente da Alphabet ed Apple.

Per sviluppare l'app del Parco digitale della biodiversità umbra abbiamo scelto uno di questi strumenti: [Apache Cordova](https://cordova.apache.org/), un ambiente di sviluppo app open source. La scelta è stata dettata dal fatto che lo strumento è open source, quindi fortemente educativo, gratuito e, soprattutto, consente di sviluppare le app mediante le tecnologie web già oggetto di apprendimento nella nostra scuola (HTML, CSS e JavaScript).

Si noti che, tra gli altri, esistono anche strumenti in grado di avvicinare gli studenti allo sviluppo di app per smartphone mediante gli ormai diffusissimi linguaggi a blocchi, come [App Inventor](https://appinventor.mit.edu/) e [App Lab](https://code.org/educate/applab).