% order5_0074  eq1=34214 eq2=37681  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(X,f(W,U))),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,f(X,Y))),W),W) )).
