% hard3_0132  eq1=1050 eq2=3320  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Y,Y)),Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(Y,f(Y,Z))) )).
