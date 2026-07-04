% order5_0048  eq1=31481 eq2=59851  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,Z),f(Z,W))),Z) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(f(X,Y),Z) = f(W,f(f(Y,U),X)) )).
