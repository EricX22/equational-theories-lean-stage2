% hard3_0026  eq1=127 eq2=2148  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,f(f(Y,Y),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Y),Z),f(Y,X)) )).
