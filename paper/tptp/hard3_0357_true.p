% hard3_0357  eq1=3417 eq2=3737  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(Z,f(Z,f(Y,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(X,Z),f(Y,Z)) )).
