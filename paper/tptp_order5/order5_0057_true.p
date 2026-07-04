% order5_0057  eq1=13026 eq2=18300  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Y,f(Z,f(X,Z))),Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,Y),f(Z,f(f(Y,Y),Y))) )).
