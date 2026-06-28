% hard3_0275  eq1=2650 eq2=3943  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(X,X),f(Y,X)),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(X,f(Z,Z)),Y) )).
