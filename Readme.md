
### Triangulo

            0
          1   2
        3   4   5
      6   7   8   9
    10  11  12  13  14

### Triangulo

                         P0   P1     P2      P3         P4        P5
#### [                          P0+i    P1+1   P1+i+1     P2+i+1     P4+1
#### 0 [0, 1, 2, 3, 4, 5]  [ 0, 0+1=1, 1+1=2, 1+1+1= 3,  2+1+1= 4,  4+1= 5]
#### 1 [1, 3, 4, 6, 7, 8]  [ 1, 1+2=3, 3+1=4, 3+2+1= 6,  4+2+1= 7,  7+1= 8]
#### 2 [2, 4, 5, 7, 8, 9]  [ 2, 2+2=4, 4+1=5, 4+2+1= 7,  5+2+1= 8,  8+1= 9]
#### 3 [3, 6, 7,10,11,12]  [ 3, 3+3=6, 6+1=7, 6+3+1=10,  7+3+1=11, 11+1=12]
#### 4 [4, 7, 8,11,12,13]  [ 4, 4+3=7, 7+1=8, 7+3+1=11,  8+3+1=12, 12+1=13]
#### 5 [5, 8, 9,12,13,14]  [ 5, 5+3=8, 8+1=9, 8+3+1=12,  9+2+1=13, 13+1=14]
#### ]

         P0-0
       P1-1  P2-2      P3 = P1+i+1
     P3-3  P4-4  P5-5    P4 = P2+i+1

   [0, 1, 3], [0, 2, 5], [3, 4, 5]]


 [
 0 [0, 1, 2, 3, 4, 5]
  0  1   3
 [P0,P1,P3]
 [


  0 {[1,3],[2,5]}
  3 {[1,0],[4,5]}
  5 {[2,0],[4,3]}


 ### 1. Backtracking (Búsqueda con retroceso)                                                                                                                                   
                                                                                                                                                                             
  - Cómo funciona: Prueba todos los movimientos posibles recursivamente, retrocede cuando no hay solución                                                                    
  - Pros: Simple, garantiza encontrar solución si existe, rápido para tableros pequeños (15 celdas = ~32,768 estados máximo)                                                 
  - Contras: No "aprende", siempre recalcula                                                                                                                                 
                                                                                                                                                                             
 ### 2. Q-Learning (Aprendizaje por refuerzo)                                                                                                                                   
                                                                                                                                                                             
  - Cómo funciona: Aprende una tabla Q que mapea (estado, acción) → valor. Se entrena jugando muchas partidas                                                                
  - Pros: Aprende política óptima, una vez entrenado es instantáneo                                                                                                          
  - Contras: Requiere entrenamiento, tabla puede ser grande                                                                                                                  
                                                                                                                                                                             
###  3. Deep Q-Network (DQN) - Red Neuronal                                                                                                                                     
                                                                                                                                                                             
  - Cómo funciona: Usa una red neuronal para aproximar los valores Q en lugar de una tabla                                                                                   
  - Pros: Generaliza mejor, escala a tableros más grandes                                                                                                                    
  - Contras: Más complejo, requiere PyTorch/TensorFlow, necesita más entrenamiento                                                                                           
                                                                                                                                                                             
###  4. Monte Carlo Tree Search (MCTS)                                                                                                                                          
                                                                                                                                                                             
  - Cómo funciona: Construye árbol de búsqueda usando simulaciones aleatorias para evaluar movimientos                                                                       
  - Pros: Balance entre exploración y explotación, usado en AlphaGo                                                                                                          
  - Contras: Más complejo de implementar                                                                                                                                     
                                                                                                                                                                             
 ### 5. A* con heurística                                                                                                                                                       
                                                                                                                                                                             
  - Cómo funciona: Búsqueda informada usando una función heurística (ej: número de fichas restantes)                                                                         
  - Pros: Eficiente, encuentra solución óptima                                                                                                                               
  - Contras: Necesita buena heurística   


