% order5_0212  eq1=13758 eq2=2604  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(X,f(f(Z,X),W)),U)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,Z),X)),W) )).
