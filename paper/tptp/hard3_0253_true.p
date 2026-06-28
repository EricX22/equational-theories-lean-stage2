% hard3_0253  eq1=2270 eq2=4288  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(Y,f(Y,Z))),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(X,Y)) = f(X,f(Z,Z)) )).
