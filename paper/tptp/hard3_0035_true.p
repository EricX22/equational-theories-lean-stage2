% hard3_0035  eq1=194 eq2=1075  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),f(Z,X)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(Y,f(f(X,f(X,Y)),X)) )).
