% hard3_0143  eq1=1096 eq2=476  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(X,f(Z,Y)),X)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(Y,f(X,f(Y,f(Y,X)))) )).
