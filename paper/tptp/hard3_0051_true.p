% hard3_0051  eq1=344 eq2=3965  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(Z,f(X,Z)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(Y,f(Y,Y)),Y) )).
