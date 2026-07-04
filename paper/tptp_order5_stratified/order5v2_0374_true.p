% order5v2_0374  eq1=7806 eq2=32208  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Y,f(f(Z,f(W,X)),Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(f(X,f(Z,Z)),W)),W) )).
