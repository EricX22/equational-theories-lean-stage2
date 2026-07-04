% order5_0135  eq1=55502 eq2=35062  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( f(X,f(Y,Z)) = f(W,f(f(W,X),U)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(f(X,Z),Z)),Z) )).
