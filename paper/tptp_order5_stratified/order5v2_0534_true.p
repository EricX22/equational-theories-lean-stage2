% order5v2_0534  eq1=13849 eq2=7647  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Y,f(f(X,Z),Z)),Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(X,f(f(Z,f(Z,Z)),Z))) )).
