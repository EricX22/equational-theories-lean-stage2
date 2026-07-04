% order5v2_0165  eq1=23843 eq2=50551  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),Z),f(W,f(U,Y))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(X,f(f(Y,Y),X)),Z) )).
