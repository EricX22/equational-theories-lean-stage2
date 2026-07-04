% order5_0052  eq1=14741 eq2=18728  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,Y),f(X,Z)),Z)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,X),f(f(X,X),f(X,Y))) )).
