% hard3_0187  eq1=1669 eq2=1472  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,Y),f(f(Z,Y),Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,Y),f(Z,f(Z,W))) )).
