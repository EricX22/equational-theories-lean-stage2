% order5_0017  eq1=10758 eq2=33551  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(f(Z,Z),W))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(Y,f(f(f(Z,W),Z),X)),U) )).
