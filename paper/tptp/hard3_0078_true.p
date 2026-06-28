% hard3_0078  eq1=556 eq2=4396  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Z,f(Y,f(X,Z)))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(X,Y)) = f(f(X,X),Y) )).
