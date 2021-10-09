


### małe zadania do ćwiczeń

* uruchomić program z tego folderu (poinstalować co trzeba)

* sprawdzić różne kombinacje funkcji do uruchamiania job-ów async... 
  i to które przed którymi się wykonują
  
* spróbować pętlę uruchamiającą 10k krótkich zadań, i zobaczyć
  czy zakończą się w miarę równocześnie
  
*  sprawdzić, że z funkcji oznaczonych async można uruchamiać kolejne 
   funkcje async ... z wait albo i bez (przez `create_task`).

* zademonstrować, że funkcje async mogą zwracać wartości przez return,  
  że te wartości można sobie potem przypisać (np. `t = await job(5)`) 
  i wykorzystywać dalej w kodzie
