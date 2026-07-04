% order5_0149  eq1=27128 eq2=26571  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(X,X)),f(X,W)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(Y,f(f(Z,W),W)),f(Z,U)) )).
