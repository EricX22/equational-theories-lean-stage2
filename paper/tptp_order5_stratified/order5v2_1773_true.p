% order5v2_1773  eq1=22804 eq2=61339  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,X)),f(f(W,Z),W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,Y),Z) = f(f(X,f(X,Z)),W) )).
