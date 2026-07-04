% order5_0236  eq1=8144 eq2=18292  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(f(W,f(W,X)),U))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(Z,f(f(X,W),Z))) )).
