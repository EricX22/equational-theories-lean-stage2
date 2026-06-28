% hard3_0368  eq1=3669 eq2=3333  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(f(X,Y),f(Y,Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(Z,f(Z,X))) )).
